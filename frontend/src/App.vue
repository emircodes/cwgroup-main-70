<template>
    <div class="gradient-bg">
        <div class="g1"></div>
        <div class="g2"></div>
        <div class="g3"></div>
        <div class="g4"></div>
        <div class="g5"></div>
        <RouterView class="flex-shrink-0" />
        
    </div>
    <main class="container pt-4">
        <div>
            {<!--<router-link
                class=""
                :to="{name: 'Main Page'}"
            >
                Main Page
            </router-link> -->}
            |
            {<!--<router-link
                class=""
                :to="{name: 'Other Page'}"
            >
                Other Page
            </router-link> -->}
        </div>

        
        
        <RouterView class="flex-shrink-0" />
    </main>
</template>


<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});

</script>

<style lang="scss">
@import "@/style.scss";

html, body, #app, main {
    height: 100%;  /* Ensure full height for all */
    margin: 0;     /* Remove default margin */
    padding: 0;    /* Remove default padding */
}

.container{
    /* background: linear-gradient(135deg, #74b9ff, #a29bfe); */
    min-height: 100vh;  /* Ensure full height */
    min-width: 100vw;  /* Ensure full width */
    
}



</style>
