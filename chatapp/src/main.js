import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import qs from 'qs'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


import {getCurDate, getSessionStorage, removeSessionStorage, setSessionStorage} from "@/common";



const app = createApp(App)

app.use(router)
app.use(ElementPlus)
app.config.globalProperties.$axios = axios
app.config.globalProperties.$qs = qs;
app.config.globalProperties.$getCurDate = getCurDate()
app.config.globalProperties.$getSessionStorage = getSessionStorage()
app.config.globalProperties.$removeSesstionStorage = removeSessionStorage()
app.config.globalProperties.$setSessionStorage = setSessionStorage()

app.mount('#app')
app.prototype.HOST = '/api';