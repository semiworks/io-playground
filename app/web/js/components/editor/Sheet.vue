<template>
	<div v-on:drop.stop="handleDrop"
		 v-on:dragover.prevent="handleDragOver"
		 v-on:mousedown="handleMouseDown"
		 class="editor-sheet">

		<block-container v-for="block in blocks" :key="block.id" :block="block" />

		<block-link ref="drawLinkElem" v-show="connectActive" :lines="drawLinkModel.lines" />

		<block-link v-for="link in links" :lines="link.lines" :key="link.id" />
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
			links: [],

			dragActive: false,

			// last mouse down coordinates
			mouseDownX: null,
			mouseDownY: null,

			// used during connecting
			fromConnector: null,
			drawLinkModel: { lines: [] }
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
			let coords = this.getCoordinatesFromEvent(ev);

			// save mouse down coordinates for later
			this.mouseDownX = coords.x;
			this.mouseDownY = coords.y;

			// select/unselect items
			let block = this.getBlockAtLocation(coords)
			if (block !== null)
			{
				if (!block.selected && !ev.shiftKey)
				{
					// deselect all bocks
					this.deselectBlocks();
				}
				// clicked on a block -> select this block
				block.selected = true;
			}
		},

		handleDragOver: function(ev)
		{
			ev.dataTransfer.dropEffect = "copy"
		},

		handleDrop: async function(ev)
		{
			let block_id = ev.dataTransfer.getData("add-block");

			// just to be sure
			this.dragActive = false;

			// get visual representation of the block from the server
			let info = await helper.fetch('editor.blockinfo', {id: block_id});
			if (typeof result === undefined)
			{
				// an error occurred
				return;
			}

			// create a new block instance
			let coords = this.getCoordinatesFromEvent(ev);
			this.blocks.push({
				id:        this.blocks.length+1, // TODO: we need something better
				x:         coords.x,
				y:         coords.y,
				text:      info.name,
				template:  info.template,
				ports:     info.ports,
				selected:  false,
				originalX: coords.x,
				originalY: coords.y
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
			let coords = this.getCoordinatesFromEvent(ev);

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
			// get local coordinates
			let coords = this.getCoordinatesFromEvent(ev);

			if (!this.dragActive)
			{
				let block = this.getBlockAtLocation(coords)
				if (block === null || !ev.shiftKey)
				{
					// deselect all other blocks
					this.deselectBlocks(block);
				}
			}

			// stop drag operation
			this.dragActive = false;
			this.mouseDownX = null;
			this.mouseDownY = null;

			// stop establishment of a link
			this.connectEnd(null);
		},

		updateLinks: function()
		{
			for (var i = 0; i < this.links.length; i++)
			{
				let from_coords = this.links[i].from.coords();
				let to_coords   = this.links[i].to.coords();

				this.links[i].lines = [
				{
					x1: from_coords.x,
					y1: from_coords.y,
					x2: to_coords.x,
					y2: to_coords.y
				}];
			}
		},

		dragStart: function(coords)
		{
			this.dragActive = true;

			// save current coordinate as mouse down coordinate in each block (used for drag operation)
			this.blocks.forEach(function(block)
			{
				block.originalX = block.x;
				block.originalY = block.y;
			});
		},

		dragOver: function(coords)
		{
			if (!this.dragActive)
			{
				// check if a dragging operation started
				if (this.mouseDownX === null || this.mouseDownY === null)
				{
					return;
				}
				if ((Math.abs(coords.x - this.mouseDownX) + Math.abs(coords.y - this.mouseDownY)) < 10)
				{
					return;
				}
				this.dragStart();
			}

			// calculate distance
			let x_delta = coords.x - this.mouseDownX;
			let y_delta = coords.y - this.mouseDownY;

			// move all selected blocks
			for (var i = 0; i < this.blocks.length; i++)
			{
				if (!this.blocks[i].selected)
				{
					continue;
				}

				// reposition the block
				let new_coords = {
					x: Math.max(0, this.blocks[i].originalX + x_delta),
					y: Math.max(0, this.blocks[i].originalY + y_delta)
				};
				this.repositionBlock(this.blocks[i], new_coords);
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

			let from_coords = this.fromConnector.coords();
			this.drawLinkModel.lines = [
				{
					x1: from_coords.x,
					y1: from_coords.y,
					x2: coords.x,
					y2: coords.y
				}
			];
		},

		connectEnd: function(connector)
		{
			// check if we released on another connector
			if (connector !== null)
			{
				let from_coords = this.fromConnector.coords();
				let to_coords   = connector.coords();

				this.links.push({
					from:  this.fromConnector,
					to:    connector,
					lines: [
					{
						id: this.links.length+1, // TODO: we need something better
						x1: from_coords.x,
						y1: from_coords.y,
						x2: to_coords.x,
						y2: to_coords.y
					}]
				});
			}

			this.fromConnector = null;
		},

		getCoordinatesFromEvent: function(ev)
		{
			let x = ev.clientX - this.$el.offsetLeft;
			let y = ev.clientY - this.$el.offsetTop;

			return { x: x, y: y };
		},

		getBlockAtLocation: function(coords)
		{
			for (var i = 0; i < this.blocks.length; i++)
			{
				if (coords.x < this.blocks[i].x) continue;
				if (coords.y < this.blocks[i].y) continue;

				if (coords.x > (this.blocks[i].x + this.blocks[i].width)) continue;
				if (coords.y > (this.blocks[i].y + this.blocks[i].height)) continue;

				return this.blocks[i];
			}

			return null;
		},

		mapCoordinates: function(component, x, y)
		{
			let comp_rect  = component.$el.getBoundingClientRect();
			let sheet_rect = this.$el.getBoundingClientRect();

			let x_mapped = (comp_rect.x - sheet_rect.x) + x;
			let y_mapped = (comp_rect.y - sheet_rect.y) + y;

			return {
				x: x_mapped,
				y: y_mapped
			}
		},

		deselectBlocks: function(exceptBlock)
		{
			// deselect all other blocks
			for (var i = 0; i < this.blocks.length; i++)
			{
				if (this.blocks[i] !== exceptBlock)
				{
					this.blocks[i].selected = false;
				}
			}
		}
	},

	components:
	{
		BlockContainer,
		BlockLink
	}
}
</script>
