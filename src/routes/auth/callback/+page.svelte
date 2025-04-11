<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { handleTokenFromUrl } from '$lib/auth';

	let loading = true;
	let error = null;

	onMount(() => {
		try {
			const currentUrl = new URL(window.location.href);
			const token = handleTokenFromUrl(currentUrl);

			if (token) {
				console.log('Authentication token verification successful');

				setTimeout(() => {
					goto('/');
				}, 1000);
			} else {
				error = 'Authentication token not found.';
				console.error('Authentication token not found. Please verify the backend URL is correct.');
				console.error('Current URL:', window.location.href);
				console.error('Backend should be running at http://localhost:3000.');
			}
		} catch (err) {
			error = 'An error occurred during authentication.';
			console.error('Exception occurred during authentication callback:', err);
		} finally {
			loading = false;
		}
	});
</script>

<div class="flex h-screen w-full flex-col items-center justify-center bg-gray-50">
	<div class="rounded-lg bg-white p-8 shadow-lg">
		{#if loading}
			<div class="flex flex-col items-center">
				<div
					class="h-10 w-10 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"
				></div>
				<p class="mt-4 text-lg">Processing authentication...</p>
			</div>
		{:else if error}
			<div class="flex flex-col items-center text-red-500">
				<svg
					class="h-10 w-10"
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
					/>
				</svg>
				<p class="mt-4 text-lg">{error}</p>
				<p class="mt-2 text-sm text-gray-600">
					Please verify that the backend server is running at http://localhost:3000.
				</p>
				<button
					class="mt-4 rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
					on:click={() => goto('/')}
				>
					Return to login page
				</button>
			</div>
		{:else}
			<div class="flex flex-col items-center text-green-500">
				<svg
					class="h-10 w-10"
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M5 13l4 4L19 7"
					/>
				</svg>
				<p class="mt-4 text-lg">Login successful! Redirecting shortly...</p>
			</div>
		{/if}
	</div>
</div>
