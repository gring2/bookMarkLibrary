<template>
  <main>
    <h4>BookMarks</h4>
  </main>
</template>

<script>
  import { Component, Vue } from 'vue-property-decorator'

  @Component({

  })
  export default class BookmarksPanel extends Vue {

  }

</script>

<style scoped lang="scss">
  main {
    width: 75%;
  ul{
    display: flex;
    align-items: center;
    justify-content: flex-start;
    flex-wrap: wrap;
    list-style-type: none;
    width: 100%;
    height: 100%;
  li{
    display: block;
  //	margin-right: 5%;
    width: 15%;
    height: 10%;
  }
  }
  }
</style>