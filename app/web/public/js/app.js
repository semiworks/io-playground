
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
            throw new Error(42);
        }

        json = await response.json()
        console.log(json)

        // NOTE json may contain 'result' if everything is ok or 'error' if an error occurred

        return json.result
    }

    let app_device = Vue.component('device-info', {
        props: ['device_id'],
        data() {
            return {
                list_idx: -1
            }
        },
        computed: {
            name: function() {
                if (this.$store.state.device_list[this.list_idx])
                {
                    return this.$store.state.device_list[this.list_idx].name;
                }
                return '';
            },
            type: function() {
                if (this.$store.state.device_list[this.list_idx])
                {
                    return this.$store.state.device_list[this.list_idx].type;
                }
                return '';
            },
            description: function() {
                if (this.$store.state.device_list[this.list_idx])
                {
                    return this.$store.state.device_list[this.list_idx].description;
                }
                return '';
            }
        },
        created() {
            (async () => {
                try {
                    let result = await rpcFetch('device_get_info', { id: this.device_id })

                    // find list entry of this device
                    this.list_idx = -1;
                    for (let i = 0; i < this.$store.state.device_list.length; i++)
                    {
                        if (this.$store.state.device_list[i].id === this.device_id)
                        {
                            this.list_idx = i;
                            break;
                        }
                    }

                    if (this.list_idx >= 0)
                    {
                        // update name & description
                        this.$store.state.device_list[this.list_idx].name        = result.name;
                        this.$store.state.device_list[this.list_idx].description = result.description;
                    }
                }
                catch (e)
                {
                    // TODO: remove from device list ?
                    console.log(e)
                }
            })();
        },
        template: `
            <div>
                [{{ device_id }}] {{ type }}
                <ul>
                    <li><strong>Name:</strong> {{ name }}</li>
                    <li><strong>Description:</strong> {{ description }}</li>
                    <li><strong>Properties:</strong> TODO ...</li>
                </ul>
            </div>
        `
    })

    let page_index_component = Vue.component('page-index', {
        template: `
            <div>
                <h3>Devices</h3>
                <ul>
                    <li v-for="device in $store.state.device_list">
                        <device-info :device_id="device.id"></device-info>
                    </li>
                </ul>

                <hr>

                <h3>TODO</h3>
                <ul>
                    <li>Adaptors with one/multiple Device(s)
                        <ul>
                            <li><strike>Yahoo Weather</strike></li>
                            <li>Fritzbox</li>
                            <li>KNX</li>
                            <li>serial port</li>
                            <li>amazon echo</li>
                            <li>ikea tadfri</li>
                            <li>THZ404</li>
                            <li><strike>Webcam</strike></li>
                        </ul>
                    </li>
                    <li>split yahoo weather in adaptor and device</li>
                    <li>Logic Editor</li>
                    <li>Visu / Dashboard ?</li>
                    <li>Archive</li>
                    <li>HTTPS</li>
                    <li>link multiple hubs</li>
                    <li>user management</li>
                    <li>scripts</li>
                </ul>
            </div>
        `,
        created() {
            (async (vue) =>
            {
                try
                {
                    result = await rpcFetch('device_get_list')

                    for (let i = 0; i < vue.$store.state.device_list.length; i++)
                    {
                        // check if this is in result
                        let found = false;
                        for (let k = 0; k < result.length; k++)
                        {
                            if (result[k].id === vue.$store.state.device_list[i].id)
                            {
                                // found it
                                found = true;

                                // update type in device list
                                vue.$store.state.device_list[i].type = result[k].type;

                                // remove from result list
                                result.slice(k, k+1);

                                // stop here
                                break;
                            }
                        }

                        if (!found)
                        {
                            // remove from store list
                            vue.$store.state.device_list.slice(i, i+1);
                        }
                    }

                    // now add everything that is left in result
                    for (let i = 0; i < result.length; i++)
                    {
                        vue.$store.state.device_list.push({ id: result[i].id, type: result[i].type });
                    }
                }
                catch (err)
                {
                    console.log("login() failed")
                }
            })(this);
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
            username :  __INITIAL_STATE__.username,

            device_list: []
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
        store: store,

        data: {
            footer_text: "... semiworks ..."
        }
    });
})();
