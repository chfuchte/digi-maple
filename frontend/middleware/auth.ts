const publicRoutes = ['/auth', '/maps']

export default defineNuxtRouteMiddleware((to) => {
    for (const route of publicRoutes) {
        if (to.path.startsWith(route) || to.path === "/") return
    }

    // check if user is authenticated
    const auth = useCurrentUserStore().getUser() !== null
    
    if (auth && to.path === '/auth') return navigateTo('/')
    else if (auth) return

    return navigateTo('/auth')
})
