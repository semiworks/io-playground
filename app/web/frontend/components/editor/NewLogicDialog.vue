<template>
	<el-dialog title="Neue Logik anlegen" :visible.sync="newLogicDialogVisible" center>
		<div>Name: <el-input v-model="logicName" autofocus></el-input></div>

		<span slot="footer" class="dialog-footer">
			<el-button @click="newLogicDialogVisible = false">Cancel</el-button>
			<el-button type="primary" @click="accept">Confirm</el-button>
		</span>
	</el-dialog>
</template>

<script>
export default
{
	name: "NewLogicDialog",

	data()
	{
		return {
			newLogicDialogVisible: false,
			logicName: ""
		}
    },

    methods:
    {
    	open: function()
    	{
    		this.newLogicDialogVisible = true;
    	},

    	close: function()
    	{
    		this.newLogicDialogVisible = false;
    	},

    	accept: function()
    	{
    		this.$emit('accepted')
    	}
    }
}
</script>