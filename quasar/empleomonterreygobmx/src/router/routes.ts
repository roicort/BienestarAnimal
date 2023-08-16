import {RouteRecordRaw} from 'vue-router'
import { baseAPIURL } from '../boot/axios'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [

      {path: '', component: () => import('src/pages/AnimalesLista.vue')},
      {path: 'animales/:id', component: () => import('src/pages/AnimalesLista.vue')},
      {path: 'animales/favoritos', component: () => import('src/pages/AnimalesFavoritos.vue')},
      {path: 'animales/favoritos/:id', component: () => import('src/pages/AnimalesFavoritos.vue')},
      {path: 'animales/adopcion', component: () => import('src/pages/PostulacionAdopcion.vue')},

      {path: 'cuenta', component: () => import('src/pages/CuentaDetalle.vue')},
      {path: 'cuenta/perfil', component: () => import('src/pages/PerfilDetalle.vue')},
      {path: 'cuenta/perfil/editar', component: () => import('pages/EditarPerfil.vue')},

      {path: 'animales/publicar', component: () => import('src/pages/PublicarAnimal.vue')},
      {path: 'animales/detalle/:id', component: () => import('src/pages/DetalleAnimal.vue')},

      {path: 'animales/publicados', component: () => import('src/pages/AnimalesPublicados.vue')},

      {path: 'asociaciones', component: () => import('src/pages/AsociacionesLista.vue')},
      {path: 'asociaciones/:id', component: () => import('src/pages/DetalleEmpresa.vue')},
      {path: 'asociaciones/centros/:id', component: () => import('src/pages/DetalleSucursales.vue')},
      {path: 'asociaciones/centros/detalle/:id', component: () => import('src/pages/EditarSucursal.vue')},
      
      {path: 'adopciones/', component: () => import('src/pages/ReclutadorPostulaciones.vue')},

      {path: 'unauthorized', component: () => import('pages/Unauthorized.vue')},
      {path: 'tablero', component: () => import('pages/Tablero.vue')},
      //{path: 'mapa', component: () => import('pages/Mapa.vue')},
      {path: 'acerca', component: () => import('pages/Acerca.vue')},
      {path: 'ayuda', component: () => import('pages/Ayuda.vue')},

      {path: 'admin', beforeEnter: () => {window.location.href = baseAPIURL.replace('/rest/v1','')+'/dadmin/'}},
      
      {
        path: '/:catchAll(.*)*',
        component: () => import('pages/Error404.vue'),
      },
    ],
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/error404',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '', component: () => import('pages/Error404.vue')},
    ],
  },
]

export default routes
