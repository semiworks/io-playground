<template>
	<div class="editor-block">
		<div class="editor-blockheader">{{ block.text }}</div>
		<block-port v-for="port in block.ports" :key="port.id" :port="port" />
	</div>
</template>

<script>
import BlockPort from './BlockPort.vue'

export default
{
	props: [ "block" ],

	components:
	{
		BlockPort
	}
}
</script>
