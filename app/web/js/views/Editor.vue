<template>
	<div class="editor-main">
		<block-list />
		<sheet />
	</div>
</template>

<script>
import Sheet from '@/components/editor/Sheet.vue'
import BlockList from '@/components/editor/BlockList.vue'

export default
{
    components:
    {
        Sheet,
        BlockList
    }
}
</script>
