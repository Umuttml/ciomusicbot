const musicService = require("../services/music.service");
const response = require("../utils/response");

exports.search = async (req,res,next)=>{

    try{

        const query=req.body.query;

        if(!query){

            return response.error(res,400,"Arama kelimesi boş.");

        }

        const result=await musicService.search(query);

        response.success(res,result);

    }catch(err){

        next(err);

    }

}