<template>
	<div v-bind:style="{ left: block.x + 'px', top: block.y + 'px' }"
		 v-on:resize="handleResize"
		 v-on:load="handleResize"
		 class="editor-blockcontainer"
		 v-bind:class="{ 'editor-selectedblock': block.selected }">

		<simple-block v-if="block.template === 'simple'" :block="block" />

	</div>
</template>

<script>
import SimpleBlock from './SimpleBlock.vue'

export default
{
	props: [ "block" ],

	mounted: function()
	{
		this.handleResize()
	},

	methods:
	{
		handleResize: function(ev)
		{
			let client_rect = this.$el.getBoundingClientRect();

			this.block.width  = client_rect.width;
			this.block.height = client_rect.height;
		}
	},

	components:
	{
		SimpleBlock
	}
}
</script>
