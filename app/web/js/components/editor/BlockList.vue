<template>
	<div class="editor-blocklist">
		<ul>
			<block-list-entry v-for="block in blocks" :key="block.id" :block="block" />
		</ul>
	</div>
</template>

<script>
import BlockListEntry from './BlockListEntry.vue'
import helper from '@/helper.js'

export default
{
	data: function() {
		return {
			blocks: []
		}
	},

	methods:
	{
		handleDragStart: function(ev)
		{
			ev.dataTransfer.setData("text", ev.target.id);
			ev.dataTransfer.effectAllowed = "copy";
		}
	},

	created: function()
	{
		let asyncInit = async() =>
		{
			// get list of all available blocks from the server (as long as it takes show a loading animation)
			await helper.fetchAndAssignData(this, 'editor.blocklist');
		};

		asyncInit();
	},

	components:
	{
		BlockListEntry
	}
}
</script>
