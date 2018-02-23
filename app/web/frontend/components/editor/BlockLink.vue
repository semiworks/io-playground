<template>
	<svg class="editor-blocklink">
		<line v-for="line in lines"
			  :x1="line.x1"
			  :y1="line.y1"
			  :x2="line.x2"
			  :y2="line.y2" style="stroke:rgb(170,170,170);stroke-width:1" />
	</svg>
</template>

<script>
export default
{
	props: ['lines'],

	data: function()
	{
		return {
		}
	}
}
</script>
