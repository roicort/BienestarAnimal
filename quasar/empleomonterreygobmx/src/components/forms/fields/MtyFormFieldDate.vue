<template>
  <q-input v-model="vmodel" outlined dense :for="props.for" mask="date" :label="props.required? '*' : ''"
           type="date" :rules="[campoRequerido]" :bottom-slots="true" style="padding-bottom: 28px;"
            @change="print($event)">
    <template v-slot:hint>
      <div class="row items-center all-pointer-events">
        <span v-if="props.required" style="color: var(--q-negative); margin-right: 4px;">*</span><span>{{props.label}}</span>
      </div>
    </template>
    <template v-slot:append>
      <q-icon name="event" class="cursor-pointer">
        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
          <q-date v-model="vmodel" mask="YYYY-MM-DD" @update:model-value="emit('update', vmodel)">
            <div class="row items-center justify-end">
              <q-btn v-close-popup label="Cerrar" color="primary" flat/>
            </div>
          </q-date>
        </q-popup-proxy>
      </q-icon>
    </template>
    <template v-slot:label>
      <div class="row items-center all-pointer-events">
        <span v-if="props.required" style="color: var(--q-negative); margin-right: 4px;">*</span>
      </div>
    </template>
  </q-input>

</template>

<script setup lang="ts">
import {ref} from 'vue';
import {print} from 'src/utils/common';

const props = defineProps({
  value: {type: String, default: ''},
  label: {type: String, default: ''},
  for: {type: String, required: true},
  required: {type: Boolean, default: false},
  required_label: {type: String, default: 'Campo requerido'},
  rules: {type: Array, default: () => []},
});
const emit = defineEmits(['hide', 'update'])

const vmodel = ref(props.value)

const campoRequerido = (val: string) => {
  if (!val && props.required) {
    return props.required_label
  }
}

</script>

<style lang="scss" scoped>
.q-field__bottom {
  padding: 2px 12px 0;
}
</style>
