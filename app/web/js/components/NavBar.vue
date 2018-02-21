<template>
	<nav>
		<div class="navbar app-container">
			<router-link :to="{ name: 'index' }" class="nav-logo-link">
				<img src="images/logo.svg" />
			</router-link>

			<router-link :to="{ name: 'editor' }" >Editor</router-link>
		</div>
	</nav>
</template>

<script>
</script>
