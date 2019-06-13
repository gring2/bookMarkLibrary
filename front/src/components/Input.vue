<template>
  <input type="text" @change="change">
</template>

<script lang="ts">
  import { Component, Prop, Vue } from 'vue-property-decorator'

  @Component
  export default class Input extends Vue {
    @Prop() private change?: () => void

  }
</script>

<style scoped lang="css">

</style>