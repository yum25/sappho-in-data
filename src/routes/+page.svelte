<script lang="ts">
	import * as d3 from 'd3';

	import type { Fragment } from '$lib/types';
	import hierarchy from '$lib/analysis/hierarchy.json';

	let svg: SVGElement;

	let innerHeight: number | undefined = undefined;
	const height = (innerHeight ?? 900) + 200;
	const width = (innerHeight ?? 900) + 200;
	const margin = 50;

	let showHierarchy = false;
	let onHoverNode: number = 0;
	let ignoreNodes: number[] = [];

	const pack = d3
		.pack()
		.size([height - margin, width - margin])
		.padding(1);

	const root = pack(
		d3
			.hierarchy(hierarchy as unknown)
			.sum((d) => (d as Fragment).size)
			.sort((a, b) => (b.value as number) - (a.value as number))
	);

	let packingData = root.descendants();

	let data = packingData.filter((d) => d.depth == 2) as d3.HierarchyCircularNode<Fragment>[];
	let clusters = packingData.filter((d) => d.depth == 1);

	const color = d3
		.scaleOrdinal<number, string>()
		.domain(clusters.map((d) => (d.data as Fragment).name))
		.range([
			'#8FBC8B', // light green
			'cornflowerblue',
			'goldenrod',
			'#8E9ED1',
			'#C3B1E1',
			'#568203',
			'#5d6d7e',
			'#5dade2',
			'#5499c7',
			'#4B6F44',
			'#452c63',
			'#5072A7',
			'#3457D5'
		]);

	const x = d3
		.scaleOrdinal<number, number>()
		.domain(clusters.map((d) => (d.data as Fragment).name))
		.range(clusters.map((d) => d.x));
	const y = d3
		.scaleOrdinal<number, number>()
		.domain(clusters.map((d) => (d.data as Fragment).name))
		.range(clusters.map((d) => d.y));

	const simulation = d3.forceSimulation(data);

	$: simulation
		.force(
			'x',
			d3
				.forceX()
				.strength(0.005)
				.x((d) => x((d as d3.HierarchyNode<Fragment>).data.group))
		)
		.force(
			'y',
			d3
				.forceY()
				.strength(0.005)
				.y((d) => y((d as d3.HierarchyNode<Fragment>).data.group))
		)
		.force(
			'collide',
			d3
				.forceCollide()
				.strength(0.1)
				.radius((d) => (d as d3.HierarchyCircularNode<Fragment>).r + 1.5)
				.iterations(1)
		); // Force that avoids circle overlapping
	$: simulation.on('tick', () => (data = data));
</script>

<svelte:window bind:innerHeight />

<main>
	<header>
		<h1><i>Sappho</i> in Data</h1>
		<address><b>@yum25</b></address>
	</header>

	<div id="cluster">
		<svg bind:this={svg} viewBox="0 0 {width} {height}">
			<defs>
				<filter id="watercolor">
					<feTurbulence type="fractalNoise" baseFrequency="0.015" numOctaves="4" />
					<feColorMatrix
						values="0 0 0 0 0, 0 0 0 0 0, 0 0 0 0 0, 0 0 0 -0.9 1.2"
						result="texture"
					/>
					<feComposite in="SourceGraphic" in2="texture" operator="in" />
					<feGaussianBlur stdDeviation="0.5" />
				</filter>
			</defs>

			<g transform="translate({margin} {margin})">
				{#if showHierarchy}
					{#each clusters as cluster}
						<circle
							r={cluster.r}
							cx={cluster.x}
							cy={cluster.y}
							fill="transparent"
							stroke="black"
							stroke-width="5"
							stroke-opacity="0.85"
						>
						</circle>
					{/each}
				{/if}

				{#each data as fragment}
					{@const r = onHoverNode == fragment.data.name ? 30 : fragment.r}
					<g
						class:fadein={!ignoreNodes.includes(fragment.data.name)}
						class:fadeout={ignoreNodes.includes(fragment.data.name)}
						filter="url(#watercolor)"
						role="none"
						on:mouseenter={() => {
							if (fragment.r < 30) {
								onHoverNode = fragment.data.name;
							}
						}}
						on:mouseleave={() => {
							if (fragment.r < 30) {
								onHoverNode = 0;
							}
						}}
					>
						<circle {r} fill={color(fragment.data.group)} cx={fragment.x} cy={fragment.y}> </circle>
						<text
							x={fragment.x}
							y={fragment.y + 4}
							text-anchor="middle"
							fill="white"
							font-size={r >= 30 ? 25 : 15}
							clip-path={`circle(${r})`}>{fragment.data.name}</text
						>
					</g>
				{/each}
			</g>
		</svg>
		<section>
			<h2>Categorizing Sappho</h2>
			<p>
				The literary corpus of Sappho is rife with references to mortals and gods alike -
				<span style="background: lightpink;">Aphrodite</span>, Gonglya, Atthis, and brimming with
				descriptions of
				<span style="background: rgb(129, 194, 129);">beauty</span> and
				<span style="background: lavender;">nature</span>.
			</p>
			<p>
				The strong thematic similarity between poems, both in who they invoke and what they describe
				makes Sappho's fragments an especially interesting subject to place in distinct categories.
				I wondered: what if I tried to group these poems using a machine learning algorithm?
			</p>
			<p>
				Through measuring the <span style="text-decoration: underline;"
					>number of words in common between fragments</span
				>
				and a little bit of math, I created a data visualization where each distinct <b>grouping</b>
				is repesented with a different <b style="color: blue;">color</b> compared to those around it.
			</p>
			<div style="margin: 2rem 0rem;">
				<input type="checkbox" id="hierarchy" bind:checked={showHierarchy} />
				<label for="hierarchy"><b>See distinct fragment groupings</b></label>
			</div>
			<p style="margin-top: 2rem;">
				These fragments are translated by <b>Anne Carson</b>, in her collection:
				<i>If Not, Winter</i>.
			</p>
			<p style="margin-top: 3rem"><i>Scroll to start exploring! ↓ </i></p>
		</section>
	</div>
</main>

<style>
	@keyframes opacity {
		0% {
			opacity: 0%;
		}
		100% {
			opacity: 100%;
		}
	}

	.fadein {
		animation: opacity 1s linear forwards;
	}

	.fadeout {
		animation: opacity 1s linear reverse forwards;
	}
	main {
		font-family: 'Merriweather';

		box-sizing: border-box;
		padding: 5px;
	}

	p {
		line-height: 1.4;
	}

	header {
		margin: 3rem;
	}
	h1 {
		margin: 0;

		font-size: 6rem;
		font-weight: 300;

		text-align: center;
		text-transform: uppercase;
	}
	address {
		font-size: 1.2rem;
		font-style: normal;
		text-align: center;
	}

	#cluster {
		display: flex;
		justify-content: center;
		align-items: center;

		height: 100%;
		width: 100%;
	}

	#cluster > svg {
		max-height: 100vh;
		min-height: 50rem;
	}

	#cluster > section {
		max-width: 25rem;
	}
</style>
