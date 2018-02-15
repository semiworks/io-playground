<template>
	<div v-on:drop="handleDrop"
		 v-on:dragover="handleDragOver"
		 v-on:mousedown.capture="handleMouseDown"
		 v-on:mousemove.capture="handleMouseMove"
		 class="editor-sheet">
		<block-container v-for="block in blocks" :key="block.id" :block="block">
		</block-container>
	</div>
</template>

<script>
import BlockContainer from './BlockContainer.vue'
import helper from '@/helper.js'

export default
{
	data: function() {
		return {
			blocks: [],

			dragActive: false,

			// last coordinates mouse down coordinates
			mouseDownX: null,
			mouseDownY: null
		}
	},

	created: function()
	{
		document.onmousemove = this.handleDocumentMouseMove;
		document.onmouseup   = this.handleDocumentMouseUp;
	},

	methods:
	{
		getCoordinates: function(ev)
		{
			let x = ev.clientX - this.$el.offsetLeft;
			let y = ev.clientY - this.$el.offsetTop;

			return { x: x, y: y };
		},

		getBlockAtLocation: function(coords)
		{
			for (var i = 0; i < this.$children.length; i++)
			{
				if (this.$children[i].$options.name !== "BlockContainer")
				{
					continue;
				}

				if (coords.x < this.$children[i].block.x) continue;
				if (coords.y < this.$children[i].block.y) continue;

				if (coords.x > (this.$children[i].block.x + this.$children[i].$el.clientWidth)) continue;
				if (coords.y > (this.$children[i].block.y + this.$children[i].$el.clientHeight)) continue;

				return this.$children[i];
			}

			return null;
		},

		handleMouseDown: function(ev)
		{
			// get local coordinates
			let coords = this.getCoordinates(ev);

			// save mouse down coordinates for later
			this.mouseDownX = coords.x;
			this.mouseDownY = coords.y;
			this.dragActive = true;

			// get block under cursor
			let block = this.getBlockAtLocation(coords)
			if (block !== null)
			{
				// select block
				block.selected = true;

				// TODO: unselect all other blocks?
			}

			// save current coordinate as mouse down coordinate in each block (used for drag operation)
			this.$children.forEach(function(item)
			{
				item.originalX = item.block.x;
				item.originalY = item.block.y;
			});
		},

		handleDragOver: function(ev)
		{
			ev.preventDefault();
			// Set the dropEffect to move
			ev.dataTransfer.dropEffect = "copy"
		},

		handleDrop: async function(ev)
		{
			ev.preventDefault();
			// Get the id of the target and add the moved element to the target's DOM
			var data = ev.dataTransfer.getData("add-block");

			// get visual representation of the block from the server
			let info = await helper.fetch('editor.blockinfo', {id: data});
			if (typeof result === undefined)
			{
				// an error occurred
				return;
			}

			// TODO: create backend for this block?
			// TODO: get mouse coordinates
			let x = ev.clientX - ev.target.offsetLeft;
			let y = ev.clientY - ev.target.offsetTop;

			this.blocks.push({
				id: this.blocks.length+1, // TODO: we need something better
				x: x,
				y: y,
				text: info.name,
				template: info.template,
				ports: info.ports
			});
		},

		handleMouseMove: function(ev)
		{
		},

		handleDocumentMouseMove: function(ev)
		{
			// check if left button is pressed and dragging is active
			if (((ev.buttons & 0x01) === 0) || !this.dragActive)
			{
				return;
			}

			// get local coordinates
			let coords = this.getCoordinates(ev);

			// calculate distance
			let x_delta = coords.x - this.mouseDownX;
			let y_delta = coords.y - this.mouseDownY;

			// move all selected blocks
			for (var i = 0; i < this.$children.length; i++)
			{
				if (this.$children[i].$options.name !== "BlockContainer")
				{
					continue;
				}

				if (!this.$children[i].selected)
				{
					continue;
				}

				// reposition the block
				this.$children[i].block.x = this.$children[i].originalX + x_delta;
				this.$children[i].block.y = this.$children[i].originalY + y_delta;
			}
		},

		handleDocumentMouseUp: function(ev)
		{
			this.dragActive = false;
		}
	},

	components:
	{
		BlockContainer
	}
}
</script>
