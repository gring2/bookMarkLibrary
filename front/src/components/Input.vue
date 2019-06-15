<template>
  <input type="text" @change="change" :placeholder='placeholder'>
</template>

<script lang="ts">
  import { Component, Prop, Vue } from 'vue-property-decorator'

  @Component
  export default class Input extends Vue {
    @Prop() private change?: () => void
    @Prop() private placeholder?: string;
  }
</script>

<style scoped lang="css">

</style>