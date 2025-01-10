<template>
  <div class="h1">
    {{ title }}
  </div>


  <LoginForm></LoginForm>
</template>

<script lang="ts">
    import { defineComponent } from "vue";
    import LoginForm from "./LoginForm.vue";

    export default defineComponent({
        data() {
            return {
                title: "hi Page",
            }
        }
    })
</script>

<style scoped>
</style>
