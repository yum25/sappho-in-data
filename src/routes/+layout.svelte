<main>
    <slot></slot>
</main>

<style>
    main {
		font-family: 'Merriweather';

		box-sizing: border-box;
		padding: 5px;
	}

    :global(h1) {
		margin: 0;

		font-size: 6rem;
		font-weight: 300;

		text-align: center;
		text-transform: uppercase;
	}

    :global(header) {
		margin: 3rem;
	}
</style>