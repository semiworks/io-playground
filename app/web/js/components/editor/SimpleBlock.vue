<template>
	<div>
		<div>{{ block.text }}</div>
		<block-port v-for="port in block.ports" :key="port.id" :port="port">
			port
		</block-port>
	</div>
</template>

<script>
import BlockPort from './BlockPort.vue'

export default
{
	props: ["block"],

	components:
	{
		BlockPort
	}
}
</script>
