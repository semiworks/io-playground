<template>
	<div class="view-container">
		<header-bar>
			<div>neue Logik anlegen</div>
		</header-bar>

		<div class="app-container content-container" style="display: flex; flex-direction: column; align-items: stretch;">

			<div>toolbar</div>

			<div style="display: flex; flex-direction: row; align-items: stretch; flex: 1;">
				<block-list></block-list>
				<sheet></sheet>
			</div>
		</div>
	</div>
</template>

<script>
import HeaderBar from '@/components/HeaderBar.vue'
import Sheet from '@/components/editor/Sheet.vue'
import BlockList from '@/components/editor/BlockList.vue'

export default
{
    components:
    {
    	HeaderBar,
        Sheet,
        BlockList
    }
}
</script>