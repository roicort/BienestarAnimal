<template>
  <q-select ref="qselectRef" v-model="vmodel" :label="props.label" :for="props.for"
            dense outlined
            :use-input="props.useInput"
            emit-value
            map-options
            :option-label="props.optionLabel"
            :option-value="props.optionValue"
            :options="filteredOptions"
            @filter="filterOptions"
            :rules="[campoRequerido]"
            @update:model-value="onModelUpdate($event)">
    <template v-slot:label>
      <div class="row items-center all-pointer-events">
        <span v-if="props.required" style="color: var(--q-negative); margin-right: 4px;">*</span>{{ props.label }}
      </div>
    </template>
  </q-select>
</template>

<script setup lang="ts">
import {ref} from 'vue';

const qselectRef = ref(null)

const props = defineProps({
  value: {type: String, default: ''},
  label: {type: String, required: true},
  for: {type: String, required: true},
  maxValues: {type: Number, default: 1},
  required: {type: Boolean, default: false},
  requiredLabel: {type: String, default: 'Campo requerido'},
  rules: {type: Array, default: () => []},
  options: {type: Array, default: () => []},
  optionLabel: {type: String, default: 'nombre'},
  optionValue: {type: String, default: 'id'},
  useInput: {type: Boolean, default: false},
});

const filteredOptions = ref([...props.options])

const vmodel = ref(props.value)

const onModelUpdate = (event: any) => {
  console.log(event)
}

const campoRequerido = (val: string) => {
  if (!val && props.required) {
    return props.requiredLabel
  }
}

const filterOptions = (val: string, update: any) => {
  if (!val) {
    update(() => filteredOptions.value = [...props.options])
  }
  update(() => {
    const needle = val.toLowerCase()
    filteredOptions.value = props.options.filter((v: any) => v[props.optionLabel].toLowerCase().indexOf(needle) > -1)
  })
}

</script>

<style lang="scss" scoped>
.q-field__bottom {
  padding: 2px 12px 0;
}
</style>
