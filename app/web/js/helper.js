
export default
{
	sleep: async function(ms)
	{
		return new Promise(resolve => setTimeout(resolve, ms));
	},

	fetch: async function(method, params)
	{
		let url = 'api?method=' + method + '&jsonrpc=2.0&id=12';
		if (typeof params !== 'undefined')
        {
            url = url + '&params=' + JSON.stringify(params)
        }

		let response = await fetch(url, { credentials: "same-origin" });
		if (response.status === 404)
		{
			// Not Found
			// TODO: display an error messagebox
			return;
		}
		else if (response.status === 403)
		{
			// Forbidden
			// TODO: display an error messagebox
			return;
		}
		else if (response.status === 500)
		{
			// Internal Server Error
			// TODO: display an error messagebox
			return;
		}

		// get response data as rpc json
		let rpc_json = await response.json()
		// get data
		return rpc_json.result
	},

	fetchAndAssignData: async function(component, method, params)
	{
		let data = await this.fetch(method, params);
		if (typeof data === undefined)
		{
			return;
		}

		// now update the object
		this.updateObject(component.$data, data)
	},

	updateObject: function(target, from)
    {
    	var self = this;

        Object.keys(target).forEach(function(key)
        {
            // delete property if set to undefined or null
            if (from[key] === undefined || from[key] === null)
            {
            	// does not exist in 'from'
            	// -> then we cannot update 'target'
            }
            // property value is object, so recurse
            else if (typeof from[key] === 'object' && !Array.isArray(from[key]))
            {
                // target property not object, overwrite with empty object
                if (!(typeof target[key] === 'object' && !Array.isArray(target[key])))
                {
                    target[key] = {}
                }

                // recurse
                self.updateObject(target[key], from[key])
            }
            // set target property to update property
            else
            {
                target[key] = from[key]
            }
        })
    }
}
