<script lang="ts">
</script>

<main>
	<header>
		<h1>BEHIND / THE / SCENES</h1>
	</header>
	<div id="container">
		<section>
			<h2>I. <br /> Measuring Fragment Similarity</h2>
			<p>
				First, I needed a way to measure how similar fragments were to each other. For simplicity, I
				decided to use <a>Jaccard Similarities</a>, a measure of how similar one document is to
				another based on how many shared words two documents share. I learned this measurement as a
				way search engines look for relevant documents in my Web Systems class, which made
				implementing and understanding it easier for this project!
			</p>
			<p>
				It is important to note the limitations of this method, which doesn't account for word
				frequency (how many times a word is repeated in a fragment) or lexical similarity (for
				example, gold or goldsandaled).
			</p>
		</section>
		<section>
			<h2>II. <br /> Categorizing Fragments</h2>
			<p>
				Next, I needed to categorize the fragments based on the Jaccard Similarity scores between
				each pair of fragments. Taking inspiration from my internship in computational biology where
				I wrote scripts to categorize chromosome shapes, I calculated a pairwise matrix of Jaccard Similarities.
			</p>
			<p>
				Then, I inputted this matrix into an <a>Hierarchical Agglomerative Clustering</a> algorithm, which 
				iteratively groups fragments based on "distance". The distance in this case is the numerical value we get
				from calculating the Jaccard Similarity.
			</p>
		</section>
		<section>
			<h2>III. <br /> Visualizing with Circle Packing</h2>
			<p>
				Lorem ipsum dolor sit amet consectetur adipisicing elit. Doloribus quae rerum, consequuntur,
				in cupiditate numquam amet aut deleniti exercitationem ut reprehenderit tempora commodi
				omnis fugiat autem quis? Sint, nam est.
			</p>
		</section>
	</div>
</main>

<style>
	h2 {
		text-align: center;
	}
	#container {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(min(350px, 100%), 1fr));
		gap: 5rem;
	}
</style>
