<template>
  <q-inner-loading :showing="true">
    <q-spinner size="5.5rem" color="accent"/>
  </q-inner-loading>
</template>

<script> 

import {defineComponent} from 'vue'

export default defineComponent({
  name: 'JobLoader',
})
</script>