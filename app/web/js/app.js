import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'

import IndexView from './views/Index.vue'
import EditorIndexView from './views/EditorIndex.vue'
import EditorNewView from './views/EditorNew.vue'

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
				path: '/editor',
				component: { template: '<router-view />' },
				children: [
					{
						name: 'editor.index',
						path: '',
						component: EditorIndexView
					},
					{
						name: 'editor.new',
						path: 'new',
						component: EditorNewView
					}
				]
			}
		]
    }),

    render: h => h(App)
})
