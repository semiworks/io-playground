
// TODO: vuex for global storage, async components for lazy loading of pages

let vue

// immediately-invoked function expression (IIFE)
(function ()
{
    async function rpcFetch(method, params)
    {
        url = '/api?method=' + method + '&jsonrpc=2.0&id=12'
        if (typeof params !== 'undefined')
        {
            url = url + '&params=' + JSON.stringify(params)
        }

        console.log("fetch "+url)
        response = await fetch(url, { credentials: "same-origin" })
        console.log(response)
        if (response.status === 405)
        {
            // not allowed (not logged in?)
            vue.$router.push({name: 'login'})
            throw 42;
        }

        json = await response.json()
        console.log(json)

        // NOTE json may contain 'result' if everything is ok or 'error' if an error occurred

        return json.result
    }

    let page_index_component = Vue.component('page-index', {
        template: `
            <div>Startseite</div>
        `,
        created() {
            console.log("start page created")
            rpcFetch('device_get_list')
                .then(result =>
                {
                    device_list = result
                })
                .catch(reason =>
                {
                    //console.error(reason)
                });
        }
    })

    let page_login_component = Vue.component('page-login',
    {
        data()
        {
            return {
                uname: '',
                passwd: ''
            }
        },
        computed:
        {
            username()
            {
                return store.state.username
            }
        },
        methods:
        {
            async login()
            {
                console.log("TODO: login with " + this.uname + ":" + this.passwd)
                try {
                    result = await rpcFetch('login', {'username': this.uname, 'password': this.passwd})

                    console.log("logged in")
                    store.commit('user_login')
                    username = result.username
                    // navigate to start page
                    vue.$router.push({name: 'index'})
                }
                catch (err)
                {
                    console.log("login() failed")
                }
            }
        },
        template: `
            <div class="panel">
                <h2>Login Form</h2>

                <form @submit.prevent="login">
                    <div class="imgcontainer">
                        <img src="/images/avatar.png" alt="Avatar" class="avatar">
                    </div>

                    <div class="container">
                        <label><b>Username</b></label>
                        <input v-model="uname" type="text" placeholder="Enter Username" name="username">

                        <label><b>Password</b></label>
                        <input v-model="passwd" type="password" placeholder="Enter Password" name="password" required>

                        <button type="submit">Login</button>
                    </div>
                </form>
            </div>
        `
    })

    Vue.component('app-nav', {
        methods:
        {
            async logout()
            {
                try {
                    await rpcFetch('logout')

                    console.log("logged out")
                    store.commit('user_logout')
                    username = ""
                    // navigate to start page
                    vue.$router.push({name: 'login'})

                }
                catch (err)
                {
                    console.log("logout() failed")
                }
            }
        },
        computed:
        {
            logged_in()
            {
                return store.state.logged_in
            },
            username()
            {
                return store.state.username
            }
        },
        template: `
            <header>
                <nav class="nav">
                    <router-link :to="{ name: 'index' }" class="nav-left"><img src="/images/logo.svg" /></router-link>
                    <router-link :to="{ name: 'index' }" class="nav-left">ioPlayground</router-link>

                    <a href="#"  v-if="logged_in" @click.self.prevent="logout" class="nav-right">Abmelden</a>
                    <router-link v-else           :to="{ name: 'login' }"      class="nav-right">Anmelden</router-link>
                    <span v-if="logged_in" class="nav-right">Hi {{ username }}</span>
                </nav>
            </header>
        `
    })

    Vue.component('app-footer', {
        props: ['footer_text'],
        template: `
            <footer id="footer">
                {{ footer_text }}
            </footer>
        `
    })

    let router = new VueRouter(
    {
        routes: [
            { path: '/',      name: "index", component: page_index_component },
            { path: '/login', name: "login", component: page_login_component }
        ]
    })

    const store = new Vuex.Store(
    {
        state:
        {
            logged_in: __INITIAL_STATE__.logged_in,
            username:  __INITIAL_STATE__.username
        },
        mutations: {
            user_login : state => state.logged_in = true,
            user_logout: state => state.logged_in = false
        }
    })

    const vue = new Vue(
    {
        el: '#main',
        router: router,

        data: {
            todo_list: [
                {
                    "text": "Adaptors with one/multiple Device(s)",
                    "items": [
                        {
                            "text": "Yahoo Weather",
                            "done": true
                        },
                        {
                            "text": "Fritzbox"
                        },
                        {
                            "text": "KNX"
                        },
                        {
                            "text": "serial port"
                        },
                        {
                            "text": "amazon echo"
                        },
                        {
                            "text": "ikea tadfri"
                        },
                        {
                            "text": "THZ404"
                        },
                        {
                            "text": "Webcam",
                            "done": true
                        }
                    ]
                },
                {
                    "text": "split yahoo weather in adaptor and device"
                },
                {
                    "text": "Logic Editor"
                },
                {
                    "text": "Visu / Dashboard ?"
                },
                {
                    "text": "Archive"
                },
                {
                    "text": "HTTPS"
                },
                {
                    "text": "link multiple hubs"
                },
                {
                    "text": "user management"
                },
                {
                    "text": "scripts"
                }
            ],
            device_list: [],
            footer_text: "... semiworks ..."
        },

        // is called right after start
        created()
        {/*
            (async (vue) =>
            {
                const response = await fetch('/api?method=device_get_list&jsonrpc=2.0&id=12');
                if (response.status == 405)
                {
                    // not logged in
                    console.log("not logged in")
                }
                json = await response.json()
                vue.device_list = json.result
            })(this);*/
        }
    });
})();
