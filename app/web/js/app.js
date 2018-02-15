import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'

import IndexView from './views/Index.vue'
import EditorView from './views/Editor.vue'

Vue.use(VueRouter)

new Vue({
    el: '#app',

    router: new VueRouter({
    	routes: [
			{
				name: 'index',
				path: '/',
				component: IndexView
			},
			{
				name: 'editor',
				path: '/editor',
				component: EditorView
			}
		]
    }),

    render: h => h(App)
})
