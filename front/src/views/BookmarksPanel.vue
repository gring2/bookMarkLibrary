<template>
  <main>
    <Input :change="(e) => {
      setUrl(e.target.value)
    }"/>
    <Input :change="(e) => {
      setTag(e.target.value)
    }"/>

    <h4>BookMarks</h4>
  </main>
</template>

<script lang=ts>
  import { Component, Vue } from 'vue-property-decorator'
  import Input from '@/components/Input.vue'


  @Component({
    components: {
      Input
    }
  })
  export default class BookmarksPanel extends Vue {
    private url?: string;
    private tag?: string;
    
    private setTag( value: string ){
      this.tag = value;
      console.log(this.tag)
    }

    private setUrl( value: string ){
      this.url = value
      console.log(this.url)

    }
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