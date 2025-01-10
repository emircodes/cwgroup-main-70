<template>
  <div class="h1">
    {{ title }}
  </div>

  <div>
    <ul class="nav nav-pills">
      <li class="nav-item">
        <a class="nav-link active" aria-current="page" onclick="">My Profile</a>
      </li>

      <li class="nav-item">
        <a class="nav-link" href="#">Link</a>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
    import { defineComponent } from "vue";

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
