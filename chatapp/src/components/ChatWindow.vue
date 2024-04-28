<template>
  <div class="chat-app">
    <!-- 左侧菜单栏 -->
    <div class="menu">
      <!-- 菜单内容 -->
      <div class="mb-2 flex items-center text-sm">
        <el-radio-group v-model="radio1" class="ml-4">
          <el-radio-button value= "0" size="default">ChatGLM</el-radio-button>
          <el-radio-button value= "1" size="default">ChatGPT</el-radio-button>
        </el-radio-group>
      </div>
      <div class="mb-2 flex items-center text-sm">
        <el-radio-group v-model="radio2" class="ml-4">
          <el-radio-button value= "0" size="default">文本输入</el-radio-button>
          <el-radio-button value= "1" size="default">Key-Value</el-radio-button>
        </el-radio-group>
      </div>
      <div class="mb-2 flex items-center text-sm">
        <el-radio-group v-model="radio3" class="ml-4">
          <el-radio-button value= "0" size="default">中文</el-radio-button>
          <el-radio-button value= "1" size="default">English</el-radio-button>
        </el-radio-group>
      </div>
      <div>
        MaximumLength<br>
        <el-input-number v-model="MaximumLength" :precision="0" :min="0" :max="2048">
        </el-input-number>
      </div>
      <div>
        Top P<br>
        <el-input-number v-model="top_p" :precision="1" :min="0" :max="1" :step="0.1">
        </el-input-number>
      </div>
      <div>
        Temperature<br>
        <el-input-number v-model="temperature" :precision="2" :min="0" :max="2048" step="0.01">
        </el-input-number>
      </div>
    </div>

    <!-- 右侧内容 -->
    <div class="content">
      <!-- 右侧聊天窗口 -->
      <div class="chat-window-container">
        <div class="chat-window" :style="{ maxHeight: chatWindowMaxHeight + 'vh' }">
          <div class="message-list" ref="messageList">
            <!-- 消息列表 -->
            <div v-for="(message, index) in messages" :key="index" class="message">
              <div class="user-info">
                <div class="avatar" style="margin-right: 10px;">
                  <div>
                    <el-avatar> {{ message.role }} </el-avatar>
                  </div>
                </div>
                <strong class="username" style="margin-top: 10px;">{{ message.role }}</strong>
              </div>
              <div v-if="message.type !== 'json'" class="text">{{ message.text }}</div>
              <div v-else>
                <pre class="language-json"><code class="language-json">{{message.text}}</code></pre>
                <a href="#" @click="downloadJsonFile">下载抽取的JSON文件</a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="mb-4">
        <div class="input-container">
          <!-- 输入框 -->
          <input type="text" v-model="inputText" @keyup.enter="handleEnterKey" class="input-box" placeholder="输入消息..." />
          <el-button
              :loading="sendingMessage"
              type="success"
              round
              @click="sendMessage"
          >
            发送消息
          </el-button>
          <!-- 如果选择了 Key-Value，则显示额外的输入框 -->
          <div v-if="radio2 === '1'" class="mb-2 flex items-center text-sm">
            <input type="text" v-model="EntityInput" @keyup.enter="handleEnterKey" class="input-box" placeholder="输入要抽取的实体列表" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import local_config from 'src/local_config.json'
import remote_config from 'src/remote_config.json'
import Prism from 'prismjs';
import 'prismjs/components/prism-json';
import 'prismjs/themes/prism.css';
import axios from 'axios';
export default {
  data() {
    return {
      messages: [], // 存储消息的数组
      inputText: '', // 输入框文本
      chatWindowMaxHeight: 90, // 聊天窗口的最大高度
      currentRole: 'User', // 当前角色，默认为用户
      openaiApiKey: remote_config.api_key, // 你的OpenAI API密钥
      sendingMessage: false, // 发送消息的加载状态
      radio1: '0', // 默认选中 ChatGLM
      radio2: '0', // 默认选中 文本输入
      radio3: '0', // 默认选中 中文
      EntityInput: "",
      MaximumLength:2048,
      temperature:0.95,
      top_p:0.7,
    };
  },
  mounted() {
    Prism.highlightAllUnder(this.$el);
  },
  methods: {
    downloadJsonFile() {
      // 创建一个 Blob 对象
      const blob = new Blob([this.messages[1].text], { type: 'application/json' });
      // 创建下载链接
      const url = window.URL.createObjectURL(blob);
      // 创建 <a> 元素
      const link = document.createElement('a');
      // 设置下载链接和文件名
      link.href = url;
      link.download = 'bot_response.json';
      // 模拟点击链接进行下载
      link.click();
      // 清除资源
      window.URL.revokeObjectURL(url);
    },
    handleEnterKey() {
      if (!this.sendingMessage) {
        this.sendMessage();
      }
    },
    modifyContent(text, entity) {
      if (this.radio3==='0'){
      return `[背景知识]:抽取与某一实体相关的 Key-Value 知识时，可以理解为从给定的数据源中提取与该实体有关的键值对信息。这些键值对可能包含有关实体的各种属性、特征或其他相关信息。
[实体]:[${entity}]
[任务]:请你根据指定的实体抽取相关的Key-Value知识。
[文本]:"""${text}"""
请根据给定的文本，提取出与[${entity}]实体相关的 Key-Value 知识。键应该是实体的属性或特征，而值应该是与该属性或特征相关联的具体信息。
[输出格式]:不要使用markdown，JSON格式,形如
"""
{
"[某个实体]":
  {
    "[特征1]":"[特征1的知识]",
    "[特征2]":"[特征2的知识]"
  },
"[某个实体]":
   {
    "[特征1]":"[特征1的知识]",
    "[特征2]":"[特征2的知识]"
  },
}
"""[某个实体]应该是你的抽取目标[${entity}]之一,你应该用中文作答
,每一个实体应该抽取多个Key-value
[提示]考虑[${entity}]最可能预期的属性或特征`}
      else if(this.radio3==='1'){
        return `Answer in English:[Background knowledge]: When extracting Key Value knowledge related to a certain entity, it can be understood as extracting key value pair information related to that entity from a given data source. These key value pairs may contain various attributes, features, or other relevant information about the entity.
[Entity]: [${entity}]
[Task]: Please extract relevant Key Value knowledge based on the specified entity.
[Text]: "" ${text} ""
Please extract Key Value knowledge related to the [${entity}] entity based on the given text. Keys should be attributes or features of entities, while values should be specific information associated with that attribute or feature.
[Output Format]: Do not use Markdown. Instead,use JSON format which shape like
""“
{
[Entity 1]:
{
"[Feature 1]": "[Knowledge of Feature 1]",
"[Feature 2]": "[Knowledge of Feature 2]"
},
[Entity 2]:
{
"[Feature 1]": "[Knowledge of Feature 1]",
"[Feature 2]": "[Knowledge of Feature 2]"
},
}
[Entity #] should be one of your extraction targets [${entity}]，Answer in English
Each entity should extract multiple Key values
[Tip] Consider the most likely expected attribute or feature of [${entity}].Answer in English`
      }
    },
    async sendMessage() {
      if (this.inputText.trim() !== '') {
        this.sendingMessage = true; // 进入加载状态
        let cur_content = this.inputText;
        if (this.radio2 === "1"){
          cur_content = this.modifyContent(this.inputText,this.EntityInput)
        }
        const message = {
          role: this.currentRole,
          text: this.inputText,
          type: 'text'
        };
        this.messages.push(message);
        this.scrollToBottom(); // 滚动到底部
        const requestBody = [{
          // 根据你的请求体结构填写相应的数据
          model: local_config.model,
          messages: [
            { role: 'user', content: cur_content }
          ],
          temperature: this.temperature,
          top_p: this.top_p,
          max_tokens: this.MaximumLength,
          radio1:this.radio1,
          radio2:this.radio2,
          entity:this.EntityInput
          // 如果有其他字段，请根据需要添加
        },{
          model: remote_config.model,
          messages: [
            ...this.messages.map(msg => ({
              role: msg.role,
              content: msg.text
            })),
            { role: 'user', content: cur_content }
          ],
          temperature: this.temperature,
          top_p: this.top_p,
          max_tokens: this.MaximumLength,
          n: 1,
          stop: null,
          radio1:this.radio1,
          radio2:this.radio2,
          entity:this.EntityInput
        }];
        this.inputText = '';
        this.EntityInput = '';
        const urls = [local_config.base_url,remote_config.base_url];
        // 发送POST请求到OpenAI的ChatGPT API
        try {
          const response = await axios.post(
              urls[this.radio1],
              requestBody[this.radio1],
              {
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${this.openaiApiKey}`
                },
                timeout: 60000 // 设置超时时间为1min
              }
          );

          // 假设响应的数据格式是 { choices: [{ message: { content: "响应的消息" } }] }
          const botMessage = {
            role: 'Bot',
            text: response.data.choices[0].message.content.trim(),
            type: 'text'
          };
          console.log(botMessage.text)
          if (this.radio2 === "1") {
            botMessage.type = 'json'
          }
          this.messages.push(botMessage);
          this.sendingMessage = false;
          this.$nextTick(() => {
            Prism.highlightAllUnder(this.$el);
          });
        } catch (error) {
          if (axios.isCancel(error)) {
            console.log('请求被取消');
          } else if (error.code === 'ECONNABORTED') {
            console.error('请求超时');
            // 处理超时错误，显示超时消息并设置 sendingMessage 变量
            const timeoutMessage = {
              role: 'System',
              text: '消息发送超时',
              type: 'text'
            };
            this.messages.push(timeoutMessage);
            this.sendingMessage = false;
          } else {
            console.error('发生错误:', error);
            // 处理其他错误
          }
        }
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        this.$refs.messageList.scrollTop = this.$refs.messageList.scrollHeight;
      });
    }
  },
};
</script>

<style scoped>
html,
body {
  overflow-x: hidden;
  overflow-y: hidden;
}
.user-info {
  display: flex;
  align-items: center;
}

.avatar {
  display: flex;
}
.avatar > div {
  flex: 1;
  text-align: center;
}



.demo-type > div:not(:last-child) {
  border-right: 1px solid var(--el-border-color);
}
.username {
  font-weight: bold; /* 使用黑体字体 */
}
.chat-app {
  display: flex;
  height: 100vh;
  overflow-y: hidden;
}

.menu {
  width: 200px; /* 左侧菜单栏宽度 */
  min-width: 200px; /* 最小宽度 */
  background-color: #f0f0f0;
  position: fixed; /* 固定定位 */
  left: 0; /* 左侧对齐 */
  top: 0; /* 顶部对齐 */
  height: 100%; /* 高度填满整个屏幕 */
}

.content {
  flex: 1; /* 自动填充剩余空间 */
  display: flex;
  flex-direction: column; /* 垂直布局 */
  margin-left: 200px; /* 留出左侧菜单栏的宽度 */
  overflow-x: auto;
  overflow-y: hidden;
}

.chat-window-container {
  position: relative; /* 相对定位 */
  flex: 1; /* 自动填充剩余空间 */
}

.chat-window {
  overflow-y: auto; /* 纵向滚动 */
}

.message-list {
  padding: 10px;
}

.message {
  margin-bottom: 10px;
}

.input-box {
  width: calc(100% - 220px); /* 输入框宽度 */
  padding: 10px;
  margin: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}


</style>
