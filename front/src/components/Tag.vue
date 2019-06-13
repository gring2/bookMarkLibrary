<template>
  <span @click="search">{{tag}}</span>
</template>

<script lang="ts">
  import {Component, Vue, Prop} from 'vue-property-decorator'

  @Component({

  })
  export default class Tag extends Vue {
    @Prop() private tag!: string

    private search() {
      console.log('search')
    }
  }
</script>

<style scoped lang="scss">
  span{
    cursor: pointer;
    &:hover{
      color: blue;
    }
  }

</style>