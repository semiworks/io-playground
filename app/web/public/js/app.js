
// immediately-invoked function expression (IIFE)
(function ()
{
    async function rpcFetch(vue)
    {
        response = await fetch('/api?method=device_get_list&jsonrpc=2.0&id=12')
        if (response.status === 405)
        {
            // not allowed (not logged in?)
            vue.$router.push({name: 'login'})
            throw 42;
        }

        json = await response.json()
        return json.result
    }

    let page_index_component = Vue.component('page-index', {
        template: `
            <div>Startseite</div>
        `,
        created() {
            console.log("start page created")
            rpcFetch(this)
                .then(result =>
                {
                    console.log(result)
                    device_list = result
                })
                .catch(reason =>
                {
                    //console.error(reason)
                });
        }
    })

    let page_login_component = Vue.component('page-login', {
        template: `
            <div>Login</div>
        `
    })

    Vue.component('app-nav', {
        template: `
            <header>
                <nav class="nav">
                    <router-link :to="{ name: 'index' }" class="nav-left"><img src="/images/logo.svg" /></router-link>
                    <router-link :to="{ name: 'index' }" class="nav-left">ioPlayground</router-link>

                    <a href="#" class="nav-right">Abmelden</a>
                    <span class="nav-right">Hi ...</span>
                    <router-link :to="{ name: 'login' }" class="nav-right">Anmelden</router-link>
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

    let router = new VueRouter({
        routes: [
            { path: '/',      name: "index", component: page_index_component },
            { path: '/login', name: "login", component: page_login_component }
        ]
    })

    let app = new Vue(
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
