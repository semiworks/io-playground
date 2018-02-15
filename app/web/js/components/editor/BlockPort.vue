<template>
	<div>
		<div>value</div>
		<block-connector :port="port" />
	</div>
</template>

<script>
import BlockConnector from "./BlockConnector.vue"

export default
{
	props: ["port"],

	components:
	{
		BlockConnector
	}
}
</script>
