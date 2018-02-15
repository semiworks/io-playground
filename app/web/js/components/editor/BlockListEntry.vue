<template>
	<li v-on:dragstart="handleDragStart" draggable="true">
		{{ block.name }}
	</li>
</template>

<script>
export default
{
	props: ['block'],

	methods:
	{
		handleDragStart: function(ev)
		{
			ev.dataTransfer.setData("add-block", this.block.id);
			ev.dataTransfer.effectAllowed = "copy";
		}
	}
}
</script>
