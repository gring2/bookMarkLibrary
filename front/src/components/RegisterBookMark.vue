<template>
  <div>
    <Input :change="(e) => { setUrl(e.target.value) }" :placeholder="'url'"
           :styles="{
                      width: '100%',
                      fontSize: '2rem',
                      height: '2rem'
                    }"
    />
    <Input :change="(e) => { setTag(e.target.value) }" :placeholder="'#tag'"
           :styles="{
                      width: '100%',
                      fontSize: '2rem',
                      height: '2rem'
                    }"

    />
    <Button
        :click="(e) => { postDatas()}"

        :class="'submit'"
        :styles="{
        fontWeight: 'normal',
        fontSize: '1.4rem',
        width: '8rem',
    }"><template v-slot:text >Susbmit</template></Button>
  </div>
</template>

<script lang=ts>
  import { Component, Vue } from 'vue-property-decorator'
  import Input from '@/components/Input.vue'
  import Button from '@/components/Button.vue'
  import {bookmarkMod} from '@/stores/modules/bookmark'

  @Component({
    components: {
      Input,
      Button
    }
  })
  export default class RegisterBookMark extends Vue {
    private url?: string
    private tags?: string

    private setTag( value: string ) {
      this.tags = value
    }

    private setUrl( value: string ) {
      this.url = value

    }

    private postDatas() {
      if(this.url){
        bookmarkMod.POST_BOOKMARK({'url': this.url, 'tags': this.tags})

      }else{
        alert('Please enter URLS')

      }
    }
  }

</script>

<style scoped lang="scss">
  div{
     padding-top: 1rem;
    *:not(:last-child) {
      margin-bottom: 0.3rem;
    }
  }
</style>
