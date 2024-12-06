<script lang="ts">
	import * as d3 from 'd3';

	let svg: SVGElement;

	let groups = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];

	// create dummy data -> just one element per circle
	let data = [
		{ name: 'A', group: 1, size: 15 },
		{ name: 'B', group: 1, size: 10 },
		{ name: 'C', group: 1, size: 25 },
		{ name: 'D', group: 1, size: 25 },
		{ name: 'E', group: 1, size: 25 },
		{ name: 'F', group: 1, size: 15 },
		{ name: 'G', group: 2, size: 35 },
		{ name: 'H', group: 2, size: 25 },
		{ name: 'I', group: 2, size: 25 },
		{ name: 'J', group: 2, size: 25 },
		{ name: 'K', group: 2, size: 15 },
		{ name: 'L', group: 2, size: 35 },
		{ name: 'M', group: 3, size: 25 },
		{ name: 'N', group: 3, size: 35 },
		{ name: 'O', group: 3, size: 25 },
		{ name: 'A', group: 4, size: 15 },
		{ name: 'B', group: 4, size: 10 },
		{ name: 'C', group: 4, size: 25 },
		{ name: 'D', group: 4, size: 25 },
		{ name: 'E', group: 4, size: 25 },
		{ name: 'F', group: 4, size: 15 },
		{ name: 'G', group: 5, size: 35 },
		{ name: 'H', group: 5, size: 25 },
		{ name: 'I', group: 5, size: 25 },
		{ name: 'J', group: 5, size: 25 },
		{ name: 'K', group: 5, size: 15 },
		{ name: 'L', group: 5, size: 35 },
		{ name: 'M', group: 6, size: 25 },
		{ name: 'N', group: 6, size: 35 },
		{ name: 'O', group: 6, size: 25 }
	];

	let displayData = [];

	function update() {
		console.log(data);
		displayData = data;
		return data;
	}

	var color = d3.scaleOrdinal().domain(groups).range(['cornflowerblue', 'goldenrod', '#8E9ED1', '#C3B1E1', '#8FBC8B', '#568203']);

	let x = d3.scaleOrdinal().domain(groups).range([220, 440, 660]);
	let y = d3
		.scaleOrdinal()
		.domain(groups)
		.range([157, 157, 157, 314, 314, 314, 471, 471, 471, 628, 628, 628, 785, 785, 785]);
	// Features of the forces applied to the nodes:
	var simulation = d3.forceSimulation(data);

	// Apply these forces to the nodes and update their positions.
	// Once the force algorithm is happy with positions ('alpha' value is low enough), simulations will stop.
	$: simulation
		.force(
			'x',
			d3
				.forceX()
				.strength(0.5)
				.x((d) => x(d.group))
		)
		.force(
			'y',
			d3
				.forceY()
				.strength(0.5)
				.y((d) => y(d.group))
		)
		.force('center', d3.forceCenter().x(500).y(500)) // Attraction to the center of the svg area
		.force('charge', d3.forceManyBody().strength(1)) // Nodes are attracted one each other of value is > 0
		.force(
			'collide',
			d3
				.forceCollide()
				.strength(0.2)
				.radius((d) => d.size + 2)
				.iterations(1)
		); // Force that avoids circle overlapping

	$: simulation.on('tick', update);
</script>

<main>
	<h1><i>Sappho</i> in Data</h1>
	<div id="cluster">
		<svg bind:this={svg} viewBox="0 0 1100 1100">
			<!-- watercolor svg filter credits to https://observablehq.com/@veltman/watercolor -->
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

			<g>
				{#each displayData as datum}
					<g filter="url(#watercolor)">
						<circle r={datum.size} fill={color(datum.group)} cx={datum.x} cy={datum.y}>
							<text> 1 </text>
						</circle>
						<text x={datum.x} y={datum.y + 4} text-anchor="middle" fill="white"> 1 </text>
					</g>
				{/each}
			</g>
		</svg>
	</div>
</main>

<style>
	main {
		font-family: 'Merriweather';

		box-sizing: border-box;
		padding: 5px;
	}
	h1 {
		font-size: 6rem;
		font-weight: 300;

		text-align: center;
		text-transform: uppercase;
	}
</style>
