<template>
  <q-input v-model="vmodel" :label="props.label" :for="props.for"
           :maxlength="props.type === 'textarea' || props.type === 'number' ? null : props.maxlength" :readonly="props.readonly"
           outlined dense :mask="props.mask" :type="props.type" :autogrow="props.type === 'textarea'"
           :min="props.min" :max="props.max"
           :rules="[campoRequerido, validarTipo]">
    <template v-slot:label>
      <div class="row items-center all-pointer-events">
        <span v-if="props.required" style="color: var(--q-negative); margin-right: 4px;">*</span>{{ props.label }}
      </div>
    </template>
  </q-input>
</template>

<script setup lang="ts">
import {ref} from 'vue';

const props = defineProps({
  value: {type: String, default: ''},
  label: {type: String, required: true},
  for: {type: String, required: true},
  maxlength: {type: Number, default: 255},
  required: {type: Boolean, default: false},
  readonly: {type: Boolean, default: false},
  requiredLabel: {type: String, default: 'Campo requerido'},
  rules: {type: Array, default: () => []},
  mask: {type: String, default: ''},
  min: {type: Number, default: null},
  max: {type: Number, default: null},
  type: {type: String, default: 'text'},
});

const vmodel = ref(props.value)

const campoRequerido = (val: string) => {
  if (!val && props.required) {
    return props.requiredLabel
  }
}

const validarTelefono = (val: string) => {
  if (val && props.type === 'tel') {
    const regex = new RegExp('^[0-9]{10}$')
    if (!regex.test(val)) {
      return 'El teléfono debe tener exactamente 10 dígitos'
    }
  }
}

const validarCP = (val: string) => {
  if (val && props.type === 'cp') {
    const regex = new RegExp('^[0-9]{5}$')
    if (!regex.test(val)) {
      return 'El código postal debe tener exactamente 5 dígitos'
    }
  }
}

const validarNumero = (numero: number) => {
  if (numero && props.type === 'number') {
    if (!!props.min && numero < props.min) {
      console.log('numero < props.min', numero, props.min)
      return `El número debe ser mayor o igual a ${props.min}`
    }
    if (!!props.max && numero > props.max) {
      console.log('numero > props.max', numero, props.max)
      return `El número debe ser menor o igual a ${props.max}`
    }
  }
}

const validarTipo = (val: string) => {
  if (props.type === 'tel') {
    return validarTelefono(val)
  }
  if (props.type === 'number') {
    return validarNumero(parseFloat(val))
  }
  if (props.type === 'cp') {
    return validarCP(val)
  }
}

</script>

<style lang="scss" scoped>
.q-field__bottom {
  padding: 2px 12px 0 !important;
}
</style>
