<template>
  <input type="text" @change="change" :placeholder='placeholder' :style="styles">
</template>

<script lang="ts">
  import { Component, Prop, Vue } from 'vue-property-decorator'

  @Component
  export default class Input extends Vue {
    @Prop() private change?: () => void
    @Prop() private placeholder?: string
    @Prop({default: () => Object.create({}) }) private styles!: object

  }
</script>

<style scoped lang="css">

</style>