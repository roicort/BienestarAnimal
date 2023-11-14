<template>
  <q-dialog v-model="pageContext.dialog">
    <q-card
      :style="'background-color: rgba(255, 240, 255, 0.75);' + 'max-width: ' + ($q.screen.gt.sm ? '' : '256px')">

      <div v-if="selectedCityName.animal_info">
        <q-img :src="selectedCityName.animal_info.foto" :ratio="1 / 1" />
      </div>

      <div style="padding: 5%;">

        <template v-if="selectedCityName.animal_info">
          <div>
            Nombre: {{ selectedCityName.animal_info.label }}
          </div>
          <div>
            Descripcion: {{ selectedCityName.animal_info.categoria_info.nombre }}
          </div>
          <div>
            Sexo: {{ selectedCityName.animal_info.sexo }}
          </div>
          <div>
            Asociacion: {{ selectedCityName.animal_info.asociacion_info.nombre }}
          </div>
        </template>

        <div>
          Descripción de los hechos: {{ selectedCityName.descripcion_hechos }}
        </div>
        <div>
          Fecha: {{ selectedCityName.fecha_reporte }}
        </div>
        <div>
          Llamar a: {{ selectedCityName.llamar_a }}
        </div>
        <div>
          Estado: {{ selectedCityName.estatus }}
        </div>
      </div>
    </q-card>
  </q-dialog>

  <ol-map ref="map" :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height: 800px">
    <ol-view ref="view" :center="center" :rotation="rotation" :zoom="zoom" :projection="projection" />

    <ol-swipe-control ref="swipeControl" v-if="layerList.length > 0" :layerList="layerList" />

    <ol-layerswitcherimage-control />

    <ol-tile-layer ref="osmLayer" title="OSM">
      <ol-source-osm />
    </ol-tile-layer>

    <ol-mouseposition-control />
    <ol-fullscreen-control />
    <ol-overviewmap-control>
      <ol-tile-layer>
        <ol-source-osm />
      </ol-tile-layer>
    </ol-overviewmap-control>

    <ol-context-menu-control :items="contextMenuItems" />

    <ol-interaction-clusterselect @select="featureSelected" :pointRadius="20">
      <ol-style>
        <ol-style-stroke color="green" :width="5"></ol-style-stroke>
        <ol-style-fill color="rgba(255,255,255,0.5)"></ol-style-fill>
      </ol-style>
    </ol-interaction-clusterselect>

    <ol-interaction-select @select="featureSelected" :condition="selectCondition" :filter="selectInteactionFilter"
      v-if="!drawEnable">
      <ol-style>
        <ol-style-stroke color="green" :width="10"></ol-style-stroke>
        <ol-style-fill color="rgba(255,255,255,0.5)"></ol-style-fill>
      </ol-style>
    </ol-interaction-select>

    <ol-overlay :position="selectedCityPosition" v-if="selectedCityName != '' && !drawEnable">
      <template v-slot="slotProps">

        <div>
          Coordenadas: {{ slotProps.position }}
        </div>
      </template>
    </ol-overlay>

    <ol-vector-layer>
      <ol-source-vector>
        <ol-feature ref="animationPath">
          <ol-geom-line-string :coordinates="path"></ol-geom-line-string>
          <ol-style-flowline color="red" color2="yellow" :width="10" :width2="10" :arrow="1" />
        </ol-feature>
        <ol-animation-path v-if="animationPath" :path="animationPath.feature" :duration="4000" :repeat="10">
          <ol-feature>
            <ol-geom-point :coordinates="path[0]"></ol-geom-point>
            <ol-style>
              <ol-style-circle :radius="10">
                <ol-style-fill color="blue"></ol-style-fill>
                <ol-style-stroke color="blue" :width="2"></ol-style-stroke>
              </ol-style-circle>
            </ol-style>
          </ol-feature>
        </ol-animation-path>
      </ol-source-vector>
    </ol-vector-layer>

    <ol-vector-image-layer>
      <ol-source-vector :url="url" :format="geoJson"> </ol-source-vector>
      <ol-style>
        <ol-style-stroke color="green" :width="5"></ol-style-stroke>
        <ol-style-fill color="rgba(255,255,255,0.5)"></ol-style-fill>
        <ol-style-icon :src="animalIcon" :scale="0.05"></ol-style-icon>
      </ol-style>
    </ol-vector-image-layer>

  </ol-map>
</template>

<script setup>
import { ref, inject, reactive } from 'vue';

import markerIcon from '/img/logos/logo_bolsa_empleo_v1.png';
import animalIcon from '/img/animal.png';

import { getPadron } from 'src/boot/utils';
import { useAuthStore } from 'stores/auth'

const center = ref([-100.31, 25.66]);
const projection = ref('EPSG:4326');
const zoom = ref(12);
const rotation = ref(0);

const format = inject('ol-format');

const url = 'http://localhost:8000/wfs/reportes/?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=reporteperdido&OUTPUTFORMAT=geojson'

const geoJson = new format.GeoJSON();

const selectConditions = inject('ol-selectconditions');

const selectCondition = selectConditions.pointerMove;

const selectedCityName = ref('');
const selectedCityPosition = ref([]);

const extent = inject('ol-extent');

const Feature = inject('ol-feature');
const Geom = inject('ol-geom');

const contextMenuItems = ref([]);
const vectorsource = ref(null);
const view = ref(null);

const drawEnable = ref(false);
const drawType = ref('Point');

const authStore = useAuthStore()

const pageContext = reactive({
  dialog: false,
})

const changeDrawType = (active, draw) => {
  drawEnable.value = active;
  drawType.value = draw;
};

contextMenuItems.value = [
  {
    text: 'Center map here',
    classname: 'some-style-class', // add some CSS rules
    callback: (val) => {
      view.value.setCenter(val.coordinate);
    }, // `center` is your callback function
  },
  {
    text: 'Add a Marker',
    classname: 'some-style-class', // you can add this icon with a CSS class
    // instead of `icon` property (see next line)
    icon: markerIcon, // this can be relative or absolute
    callback: (val) => {
      console.log(val);
      const feature = new Feature({
        geometry: new Geom.Point(val.coordinate),
      });
      vectorsource.value.source.addFeature(feature);
    },
  },
  '-', // this is a separator
];

const featureSelected = (event) => {
  if (event.selected.length == 1) {
    selectedCityPosition.value = extent.getCenter(
      event.selected[0].getGeometry().extent_,
    );
    selectedCityName.value = event.selected[0].values_;
    console.log(event.selected[0].values_);
    getPadron(authStore.firebaseUserData.accessToken, selectedCityName.value.animal_id).then((padron) => {
      selectedCityName.value.animal_info = padron;
      console.log(selectedCityName);
      pageContext.dialog = true;
    });
  } else {
    selectedCityName.value = '';
  }
};

const overrideStyleFunction = (feature, style) => {
  const clusteredFeatures = feature.get('features');
  const size = clusteredFeatures.length;

  const color = size > 20 ? '192,0,0' : size > 8 ? '255,128,0' : '0,128,0';
  const radius = Math.max(8, Math.min(size, 20));
  const dash = (2 * Math.PI * radius) / 6;
  const calculatedDash = [0, dash, dash, dash, dash, dash, dash];

  style.getImage().getStroke().setLineDash(dash);
  style
    .getImage()
    .getStroke()
    .setColor('rgba(' + color + ',0.5)');
  style.getImage().getStroke().setLineDash(calculatedDash);
  style
    .getImage()
    .getFill()
    .setColor('rgba(' + color + ',1)');

  style.getImage().setRadius(radius);

  style.getText().setText(size.toString());
};

const selectInteactionFilter = (feature) => {
  return feature.values_.name != undefined;
};

const getRandomInRange = (from, to, fixed) => {
  return (Math.random() * (to - from) + from).toFixed(fixed) * 1;
};

const drawstart = (event) => {
  console.log(event);
};

const drawend = (event) => {
  console.log(event);
};

const modifystart = (event) => {
  console.log(event);
};

const modifyend = (event) => {
  console.log(event);
};

const videoStopped = (event) => {
  console.log(event);
};

const swipeControl = ref(null);
const osmLayer = ref(null);
const layerList = ref([]);

const path = ref([
  [-100.3564453125, 25.76302734375001],
  [-100.2764453125, 25.74302734375001],
]);
const animationPath = ref(null);

</script>