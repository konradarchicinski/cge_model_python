% rebase('base.tpl', title='Python')
<div class="row">
	<div class="col-md-12">
  
<h1>
  CGE modelling in Python
</h1>
<p>
  Welcome to our CGE model written completely in Python language. We are students from Faculty of Economic Sciences, University of Warsaw. <br>
  The above model was the part of final project for one of our courses during studies.
</p>
<form action="/formProcess", method="POST">
  <fieldset>
    <legend>
      <h2>
        General information
      </h2>
    </legend>
    <div class="control">
      <label for="name">File name:<br></label><input type="text" name="file_name" value=""/>
    </div>
    <div class="control">
      <label for="name">Sheet name:<br></label><input type="text" name="sheet_name" value=""/>
    </div>
    <div class="control">
      <label for="name">Setting name:<br></label><input type="text" name="setting_name" value=""/>
    </div>
    <br>
    <fieldset>
      <legend>Year 2020:</legend>
      <div class="control">
        <label for="name">Capital shock: </label><input type="float" name="cap_shock_2020" value=""/>
      </div>
      <div class="control">
        <label for="name">Labour shock: </label><input type="float" name="lab_shock_2020" value=""/>
      </div>
    </fieldset>
    <fieldset>
      <legend>Year 2021:</legend>
      <div class="control">
        <label for="name">Capital shock: </label><input type="float" name="cap_shock_2021" value=""/>
      </div>
      <div class="control">
        <label for="name">Labour shock: </label><input type="float" name="lab_shock_2021" value=""/>
      </div>
    </fieldset>
    <fieldset>
      <legend>Year 2022:</legend>
      <div class="control">
        <label for="name">Capital shock: </label><input type="float" name="cap_shock_2022" value=""/>
      </div>
      <div class="control">
        <label for="name">Labour shock: </label><input type="float" name="lab_shock_2022" value=""/>
      </div>
    </fieldset>
    <fieldset>
      <legend>Year 2023:</legend>
      <div class="control">
        <label for="name">Capital shock: </label><input type="float" name="cap_shock_2023" value=""/>
      </div>
      <div class="control">
        <label for="name">Labour shock: </label><input type="float" name="lab_shock_2023" value=""/>
      </div>
    </fieldset>
    <fieldset>
      <legend>Year 2024:</legend>
       <div class="control">
        <label for="name">Capital shock: </label><input type="float" name="cap_shock_2024" value=""/>
      </div>
      <div class="control">
        <label for="name">Labour shock: </label><input type="float" name="lab_shock_2024" value=""/>
      </div>
    </fieldset>
    <br>
    <div class="control">
      <input type="submit" value="Submit" />
    </div>
  </fieldset>
</form> 
	
	
	
	</div>
</div>
