<template>
  <div class="row ">
    <div class="col">

      <ol-map :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height: 33rem; width: 100%;">

        <ol-view ref="view" :center="componentContext.center" :rotation="componentContext.rotation" :zoom="componentContext.zoom"
          :projection="componentContext.projection" renderer="canvas" />

        <ol-tile-layer>
          <ol-source-osm />
        </ol-tile-layer>

        <ol-vector-layer>
          <ol-source-vector>

            <template v-if="componentContext.center"> 
            <ol-feature >
              <ol-geom-circle :center="componentContext.center" :radius="0.005"></ol-geom-circle>
              <ol-style>
                <ol-style-stroke color="blue" :width="0.5"></ol-style-stroke>
                <ol-style-fill color="rgba(0,0,255,0.1)"></ol-style-fill>
              </ol-style>
            </ol-feature>

              <ol-feature>
                <ol-geom-point :coordinates="componentContext.center"></ol-geom-point>
              </ol-feature>

            </template>

            <template v-if="componentContext.objkts">

              <ol-feature v-for="(objkt, index) in componentContext.objkts" :key="index">
                <ol-geom-point :coordinates="objkt.coords"></ol-geom-point>
              </ol-feature>

            </template> 

          </ol-source-vector>
        </ol-vector-layer>

        <ol-vector-layer>
          <ol-source-vector :url="componentContext.geojson" :format="geoJSON"> </ol-source-vector>
        </ol-vector-layer>

        <ol-overlay
          v-if="componentContext.selected"
          :position="componentContext.selected_coords"
        >
            <template v-slot="slotProps">
            <div class="overlay-content" v-if="slotProps">
              <q-chip>
                {{ componentContext.selected }}
              </q-chip>
            </div>
          </template>
        </ol-overlay>

        <ol-interaction-select
          @select="featureSelected"
        >
          <ol-style>
            <ol-style-stroke color="green" :width="10"></ol-style-stroke>
            <ol-style-fill color="rgba(255,255,255,0.5)"></ol-style-fill>
          </ol-style>
        </ol-interaction-select>

      </ol-map>

    </div>
  </div>
</template>

<script setup lang="ts">

import { reactive, inject } from 'vue';
const extent = inject('ol-extent');
const format = inject('ol-format');
const geoJSON = new format.GeoJSON();

const props = defineProps({
  center: { type: ArrayBuffer},
  projection: { type: String, default: 'EPSG:4326' },
  zoom: { type: Number, default: 15},
  rotation: { type: Number, default: 0 },
  objkts: { type: ArrayBuffer, default: [] },
  geojson: { type: Object, default: null },
});

const componentContext = reactive({
  center: props.center,
  projection: props.projection,
  zoom: props.zoom,
  rotation: props.rotation,
  objkts: props.objkts,
  selected: {},
  geojson: props.geojson,
});

if(!componentContext.center){
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(setCenter);
  }
}

function setCenter(position: any) {
  componentContext.center = [position.coords.longitude, position.coords.latitude];
}

const featureSelected = (event: any) => {
  if (event.selected.length == 1) {
    componentContext.selected_coords = extent.getCenter(
      event.selected[0].getGeometry().extent_
    );
    componentContext.selected = event.selected[0].values_
    if(componentContext.selected.nombre != undefined){
      console.log(componentContext.selected)
    }
  }
};


</script>