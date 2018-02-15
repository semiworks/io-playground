<template>
	<div v-bind:style="{ left: block.x + 'px', top: block.y + 'px' }"
		 class="editor-blockcontainer">

		<simple-block v-if="block.template === 'simple'" :block="block" />

	</div>
</template>

<script>
import SimpleBlock from './SimpleBlock.vue'

export default
{
	name: "BlockContainer",

	data: function()
	{
		return {
			selected: false,

			// coordinates of the block when the mouse is pressed
			originalX: null,
			originalY: null
		}
	},

	props: ["block"],

	methods:
	{
	},

	components:
	{
		SimpleBlock
	}
}
</script>
