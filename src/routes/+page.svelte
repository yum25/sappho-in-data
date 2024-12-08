<script lang="ts">
	import * as d3 from 'd3';

	import type { Fragment } from '$lib/types';
	import hierarchy from '$lib/analysis/hierarchy.json';

	let svg: SVGElement;

	const height = 1100;
	const width = 1100;
	const margin = 50;

	const pack = d3
		.pack()
		.size([height - margin, width - margin])
		.padding(1);

	const root = pack(
		d3
			.hierarchy(hierarchy as unknown)
			.sum((d) => (d as Fragment).size)
			.sort((a, b) => b.data.size - a.data.size)
	);

	let packingData = root.descendants();

	let data = packingData.filter((d) => d.depth == 2) as d3.HierarchyCircularNode<Fragment>[];
	let posMappings = packingData.filter((d) => d.depth == 1);

	console.log(root);

	const color = d3
		.scaleOrdinal()
		.domain(posMappings.map((d) => (d.data as Fragment).name) as Iterable<string>)
		.range(['#8FBC8B', 'cornflowerblue', 'goldenrod', '#8E9ED1', '#C3B1E1', '#568203']);
	const x = d3
		.scaleOrdinal()
		.domain(posMappings.map((d) => (d.data as Fragment).name) as Iterable<string>)
		.range(posMappings.map((d) => d.x));
	const y = d3
		.scaleOrdinal()
		.domain(posMappings.map((d) => (d.data as Fragment).name) as Iterable<string>)
		.range(posMappings.map((d) => d.y));

	const simulation = d3.forceSimulation(data);

	$: simulation
		.force(
			'x',
			d3
				.forceX()
				.strength(0.75)
				.x((d) => x((d as d3.HierarchyNode<Fragment>).data.group.toString()) as number)
		)
		.force(
			'y',
			d3
				.forceY()
				.strength(0.75)
				.y((d) => y((d as d3.HierarchyNode<Fragment>).data.group.toString()) as number)
		)
		.force(
			'center',
			d3
				.forceCenter()
				.x(width / 2)
				.y(height / 2)
		) // Attraction to the center of the svg area
		.force('charge', d3.forceManyBody().strength(1)) // Nodes are attracted one each other of value is > 0
		.force(
			'collide',
			d3
				.forceCollide()
				.strength(0.4)
				.radius((d) => (d as d3.HierarchyNode<Fragment>).r + 5)
				.iterations(1)
		); // Force that avoids circle overlapping
	$: simulation.on('tick', () => (data = data));
</script>

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
				{#each data as fragment}
					<g filter="url(#watercolor)">
						<circle
							r={fragment.r}
							fill={color(fragment.data.group)}
							cx={fragment.x}
							cy={fragment.y}
						>
						</circle>
						<text x={fragment.x} y={fragment.y + 4} text-anchor="middle" fill="white"
							>{fragment.data.name}</text
						>
					</g>
				{/each}
			</g>
		</svg>
		<section>
			<h2>Lorem Ipsum Dolor Sit</h2>
			<p>
				Lorem, ipsum dolor sit amet consectetur adipisicing elit. Rem et unde optio ducimus, dolorem
				obcaecati saepe suscipit maiores incidunt neque quasi eveniet blanditiis odit dicta, ipsum
				minus nisi quia deleniti!
			</p>
			<p>
				Lorem, ipsum dolor sit amet consectetur adipisicing elit. Rem et unde optio ducimus, dolorem
				obcaecati saepe suscipit maiores incidunt neque quasi eveniet blanditiis odit dicta, ipsum
				minus nisi quia deleniti!
			</p>
			<p>
				Lorem, ipsum dolor sit amet consectetur adipisicing elit. Rem et unde optio ducimus, dolorem
				obcaecati saepe suscipit maiores incidunt neque quasi eveniet blanditiis odit dicta, ipsum
				minus nisi quia deleniti!
			</p>
			<h2>Lorem Ipsum Dolor Sit</h2>
			<p>
				Lorem, ipsum dolor sit amet consectetur adipisicing elit. Rem et unde optio ducimus, dolorem
				obcaecati saepe suscipit maiores incidunt neque quasi eveniet blanditiis odit dicta, ipsum
				minus nisi quia deleniti!
			</p>
			<p>
				Lorem, ipsum dolor sit amet consectetur adipisicing elit. Rem et unde optio ducimus, dolorem
				obcaecati saepe suscipit maiores incidunt neque quasi eveniet blanditiis odit dicta, ipsum
				minus nisi quia deleniti!
			</p>
			<p>
				Lorem, ipsum dolor sit amet consectetur adipisicing elit. Rem et unde optio ducimus, dolorem
				obcaecati saepe suscipit maiores incidunt neque quasi eveniet blanditiis odit dicta, ipsum
				minus nisi quia deleniti!
			</p>
		</section>
	</div>
</main>

<style>
	main {
		font-family: 'Merriweather';

		box-sizing: border-box;
		padding: 5px;
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
	}

	#cluster > svg {
		max-height: 100vh;
		min-height: 60vh;
	}

	#cluster > section {
		max-width: 30rem;
	}
</style>
