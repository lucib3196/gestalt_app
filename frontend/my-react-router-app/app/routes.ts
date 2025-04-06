import { type RouteConfig, route, layout } from '@react-router/dev/routes';

export default [
  layout('layouts/MainLayout.tsx', [
    route('/', 'routes/Home.tsx'),
    route('about', 'routes/About.tsx'),
    route('contact', 'routes/Contact.tsx'),
    route('generator', 'routes/Generator.tsx'),
    route('codeEditor', 'routes/CodeEditorPage.tsx'),
    route('module', 'routes/ModulePage.tsx'),
    route('module/:id', "routes/ModuleDetails.tsx")
  ]),
] satisfies RouteConfig;