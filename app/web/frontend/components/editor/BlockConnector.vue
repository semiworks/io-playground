<template>
	<div class="editor-connector"
		 v-on:mousedown.stop="handleMouseDown"
	     v-on:mouseup.stop="handleMouseUp">
		&#x26AC;
	</div>
</template>

<script>
import helper from "@/helper.js"

export default
{
	props: [ "port"],

	methods:
	{
		coords: function()
		{
			let sheet = helper.getSheet(this);
			return sheet.mapCoordinates(this, this.$el.clientWidth/2, this.$el.clientHeight/2);
		},

		handleMouseDown: function(ev)
		{
			let sheet = helper.getSheet(this);
			sheet.connectStart(this);
		},

		handleMouseUp: function(ev)
		{
			let sheet = helper.getSheet(this);
			sheet.connectEnd(this);
		}
	}
}
</script>
