
// immediately-invoked function expression (IIFE)
(function ()
{
    var app = new Vue(
    {
        el: '#main',

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
        mounted()
        {
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
            })(this);
        }
    });
})();
