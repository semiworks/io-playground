<template>
    <div id="app">
        <nav-bar />

		<section class="app-container view-container">
			<router-view></router-view>
		</section>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default
{
    components:
    {
        NavBar
    }
}
</script>
