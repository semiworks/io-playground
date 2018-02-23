<template>
	<div v-bind:class="{ 'editor-blockport-in': (port.type === 'in'), 'editor-blockport-out': (port.type === 'out'), 'editor-blockport-inout': (port.type === 'inout') }"
		 class="editor-blockport">
		<block-connector v-if="port.type === 'inout' || port.type === 'in'" :port="port" />
		<div class="editor-blockport-text">{{ port.name }}</div>
		<block-connector v-if="port.type === 'inout' || port.type === 'out'" :port="port" />
	</div>
</template>

<script>
import BlockConnector from "./BlockConnector.vue"

export default
{
	props: [ "port" ],

	components:
	{
		BlockConnector
	}
}
</script>
