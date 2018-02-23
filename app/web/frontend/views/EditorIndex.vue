<template>
	<div class="view-container">
		<header-bar>
			<div>Übersicht aller Logiken</div>
		</header-bar>

		<div class="app-container content-container">
			<el-button type="text" @click="openNewLogicDialog">Neue Logik anlegen</el-button>
		</div>

		<new-logic-dialog
			ref="new_logic_dialog"
			v-on:accepted="handleNewLogicDialogAccepted" />
	</div>
</template>

<script>
import HeaderBar from '@/components/HeaderBar.vue'
import NewLogicDialog from '@/components/editor/NewLogicDialog.vue'

export default
{
	data()
	{
		return {
			newLogicDialogVisible: false
		}
    },

    methods:
    {
    	openNewLogicDialog: function()
    	{
    		this.$refs.new_logic_dialog.open();
    	},

    	handleNewLogicDialogAccepted: function()
    	{
    		console.log(this.$refs.new_logic_dialog.logicName);
    		this.$refs.new_logic_dialog.close();
    	}
    },

    components:
    {
    	HeaderBar,
    	NewLogicDialog
    }
}
</script>
