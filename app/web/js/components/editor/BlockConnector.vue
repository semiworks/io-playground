<template>
	<div v-on:mousedown.stop="handleMouseDown"
	     v-on:mouseup.stop="handleMouseUp">
		x
	</div>
</template>

<script>
import helper from "@/helper.js"

export default
{
	props: ["port"],

	methods:
	{
		handleMouseDown: function(ev)
		{
			let sheet = helper.getSheet(this);
			sheet.connectStart(this);
		},

		handleMouseUp: function(ev)
		{
			console.log('block connector: handleMouseUp');
			let sheet = helper.getSheet(this);
			sheet.connectEnd(this);
		}
	}
}
</script>
