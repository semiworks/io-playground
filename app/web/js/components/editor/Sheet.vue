<template>
	<div v-on:drop.stop="handleDrop"
		 v-on:dragover.prevent="handleDragOver"
		 v-on:mousedown="handleMouseDown"
		 class="editor-sheet">
		<block-container v-for="block in blocks" :key="block.id" :block="block">
		</block-container>

		<block-link ref="drawLinkElem" v-show="connectActive" />
	</div>
</template>

<script>
import BlockContainer from './BlockContainer.vue'
import BlockLink from './BlockLink.vue'
import helper from '@/helper.js'

export default
{
	name: "Sheet",

	data: function()
	{
		return {
			blocks: [],

			dragActive: false,

			// last coordinates mouse down coordinates
			mouseDownX: null,
			mouseDownY: null,

			fromConnector: null
		}
	},

	computed:
	{
		connectActive: function()
		{
			return this.fromConnector !== null;
		}
	},

	created: function()
	{
		document.onmousemove = this.handleDocumentMouseMove;
		document.onmouseup   = this.handleDocumentMouseUp;
	},

	methods:
	{
		handleMouseDown: function(ev)
		{
			// check if left button is pressed and dragging is active
			if ((ev.buttons & 0x01) === 0)
			{
				return;
			}

			// get local coordinates
			let coords = this.getCoordinates(ev);

			// select/unselect items
			let block = this.getBlockAtLocation(coords)
			if (block !== null)
			{
				// clicked on a block
				// -> select this block
				block.selected = true;

				// TODO: unselect all other blocks?
			}

			// initialize drag operation
			this.dragStart(coords);
		},

		handleDragOver: function(ev)
		{
			ev.dataTransfer.dropEffect = "copy"
		},

		handleDrop: async function(ev)
		{
			let block_id = ev.dataTransfer.getData("add-block");

			// get visual representation of the block from the server
			let info = await helper.fetch('editor.blockinfo', {id: block_id});
			if (typeof result === undefined)
			{
				// an error occurred
				return;
			}

			// TODO: create backend for this block?
			let coords = this.getCoordinates(ev);

			this.blocks.push({
				id: this.blocks.length+1, // TODO: we need something better
				x: coords.x,
				y: coords.y,
				text: info.name,
				template: info.template,
				ports: info.ports
			});
		},

		handleDocumentMouseMove: function(ev)
		{
			// check if left button is pressed and dragging is active
			if ((ev.buttons & 0x01) === 0)
			{
				return;
			}

			// get local coordinates
			let coords = this.getCoordinates(ev);

			// handle dragging
			this.dragOver(coords);

			// handle establishing a connection
			this.connectUpdate(coords);
		},

		repositionBlock: function(block, coords)
		{
			block.x = coords.x;
			block.y = coords.y;

			this.updateLinks();
		},

		handleDocumentMouseUp: function(ev)
		{
			console.log('document: handleMouseUp');

			// get local coordinates
			let coords = this.getCoordinates(ev);

			// stop drag operation
			this.dragActive = false;

			// stop establishment of a link
			this.connectEnd(null);
		},

		updateLinks: function()
		{
			console.log("updateLinks()");
		},

		dragStart: function(coords)
		{
			// save mouse down coordinates for later
			this.mouseDownX = coords.x;
			this.mouseDownY = coords.y;
			this.dragActive = true;

			// save current coordinate as mouse down coordinate in each block (used for drag operation)
			this.$children.forEach(function(item)
			{
				if (item.$options.name === "BlockContainer")
				{
					item.originalX = item.block.x;
					item.originalY = item.block.y;
				}
			});
		},

		dragOver: function(coords)
		{
			if (!this.dragActive)
			{
				return;
			}

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
				this.repositionBlock(this.$children[i].block, {
					x: this.$children[i].originalX + x_delta,
					y: this.$children[i].originalY + y_delta
				});
			}
		},

		connectStart: function(connector)
		{
			this.fromConnector = connector
		},

		connectUpdate: function(coords)
		{
			if (!this.connectActive)
			{
				return;
			}

			let connector_rect = this.fromConnector.$el.getBoundingClientRect();
			let sheet_rect = this.$el.getBoundingClientRect();

			let from_x = connector_rect.x - sheet_rect.x;
			let from_y = connector_rect.y - sheet_rect.y;

			this.$refs.drawLinkElem.lines = [
				{
					x1: from_x,
					y1: from_y,
					x2: coords.x,
					y2: coords.y
				}
			];

			console.log("connect from (x="+from_x+", y="+from_y+") to (x="+coords.x+", y="+coords.y+")");
		},

		connectEnd: function(connector)
		{
			// check if we released on another connector
			if (connector !== null)
			{
				console.log('establish a permanent connection')
			}

			this.fromConnector = null;
		},

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
		}
	},

	components:
	{
		BlockContainer,
		BlockLink
	}
}
</script>
